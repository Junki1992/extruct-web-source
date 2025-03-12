import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import re
from urllib.parse import urljoin
import sys

def download_external_resource(base_url, url):
    """
    外部リソース（CSS/JS）をダウンロードします
    """
    if not url:
        return ""
    if url.startswith('//'):
        url = 'https:' + url
    elif not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding  # エンコーディングを自動判定
        return response.text
    except Exception as e:
        print(f'警告: {url} の取得に失敗しました: {str(e)}')
        return ""

def validate_url(url):
    """
    URLが有効な形式かチェックします
    """
    if not url:
        return False
    return url.startswith(('http://', 'https://'))

def get_page_source(url, combine=True):
    """
    指定されたURLのページソースを取得し、解析します
    combine: Trueの場合、全てのリソースを1つのHTMLファイルにまとめます
    """
    if not validate_url(url):
        print('エラー: 無効なURLです。"http://" または "https://" で始まるURLを入力してください。')
        return False

    try:
        # ヘッダーを設定してリクエストを送信
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding  # エンコーディングを自動判定
        response.raise_for_status()

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # メタタグでエンコーディングを指定
        meta_charset = soup.find('meta', charset=True)
        if meta_charset:
            meta_charset['charset'] = 'UTF-8'
        else:
            # charsetメタタグがない場合は追加
            meta = soup.new_tag('meta')
            meta['charset'] = 'UTF-8'
            if soup.head:
                soup.head.insert(0, meta)
            else:
                head = soup.new_tag('head')
                head.append(meta)
                soup.html.insert(0, head)

        # 結果を保存するディレクトリを作成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f'output_{timestamp}'
        os.makedirs(output_dir, exist_ok=True)

        if combine:
            # 外部スタイルシートを取得してインライン化
            for link in soup.find_all('link', rel='stylesheet'):
                css_content = download_external_resource(url, link.get('href'))
                if css_content:
                    # 既存のlinkタグを新しいstyleタグに置き換え
                    new_style = soup.new_tag('style')
                    new_style.string = css_content
                    link.replace_with(new_style)

            # 外部JavaScriptを取得してインライン化
            for script in soup.find_all('script', src=True):
                js_content = download_external_resource(url, script.get('src'))
                if js_content:
                    # srcを削除し、コンテンツをインライン化
                    del script['src']
                    script.string = js_content

            # 結合されたファイルを保存（BOMなしUTF-8で保存）
            with open(f'{output_dir}/combined.html', 'w', encoding='utf-8-sig') as f:
                f.write('<!DOCTYPE html>\n')  # DOCTYPE宣言を追加
                f.write(soup.prettify())

            print(f'結合されたファイルが {output_dir}/combined.html に保存されました。')

        else:
            # 個別のファイルとして保存（既存の処理）
            with open(f'{output_dir}/page.html', 'w', encoding='utf-8-sig') as f:
                f.write('<!DOCTYPE html>\n')  # DOCTYPE宣言を追加
                f.write(soup.prettify())

            scripts = soup.find_all('script')
            for i, script in enumerate(scripts):
                if script.string:
                    with open(f'{output_dir}/script_{i}.js', 'w', encoding='utf-8-sig') as f:
                        f.write(script.string)

            styles = soup.find_all('style')
            for i, style in enumerate(styles):
                if style.string:
                    with open(f'{output_dir}/style_{i}.css', 'w', encoding='utf-8-sig') as f:
                        f.write(style.string)

            resources = {
                'scripts': [s.get('src') for s in soup.find_all('script', src=True)],
                'styles': [s.get('href') for s in soup.find_all('link', rel='stylesheet')],
                'images': [img.get('src') for img in soup.find_all('img')],
            }

            with open(f'{output_dir}/resources.json', 'w', encoding='utf-8-sig') as f:
                json.dump(resources, f, indent=2, ensure_ascii=False)

            print(f'ソースコードの取得が完了しました。結果は {output_dir} ディレクトリに保存されています。')

        return True

    except Exception as e:
        print(f'エラーが発生しました: {str(e)}')
        return False

def main():
    """
    メイン処理：URLの入力を受け付け、ソースコードを取得します
    """
    print('Webページソース取得ツール')
    print('終了するには "exit" または "quit" と入力してください')

    while True:
        url = input('\nURLを入力してください: ').strip()

        if url.lower() in ['exit', 'quit']:
            print('プログラムを終了します')
            break

        if not url:
            print('URLを入力してください')
            continue

        combine = input('全てのリソースを1つのファイルにまとめますか？ (y/n): ').strip().lower() == 'y'
        get_page_source(url, combine)

if __name__ == '__main__':
    main()
