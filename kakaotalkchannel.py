import re
import os
import pytesseract
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 Slack API 토큰 가져오기
SLACK_SEND_URL = os.getenv("SLACK_SEND_URL")


class KakaoTalkChannel:
    """
    `KakaoTalkChannel` 카카오톡 채널 관련 기능

    ## Example

    ```python
    from kakaotalkchannel import KakaoTalkChannel

    channel_url = 'http://pf.kakao.com/_xxxxx'
    image_url = KakaoTalkChannel.get_profile_image(channel_url)
    image_text = KakaoTalkChannel.image_to_string(image_url)
    KakaoTalkChannel.send_slack(image_text)
    ```
    """

    @staticmethod
    def get_profile_image(channel_url, image_type="medium"):
        """
        `KakaoTalkChannel.get_profile_image` 카카오톡 채널에서 og meta 정보 `og:image` 공유 이미지 주소 가져오기

        ## Example

        ```python
        from kakaotalkchannel import KakaoTalkChannel

        channel_url = 'http://pf.kakao.com/_xxxxx'
        image_url = KakaoTalkChannel.get_profile_image(channel_url, image_type='large')  # large, medium, small
        ```
        """

        # 웹 페이지 소스코드 가져오기
        response = requests.get(channel_url)
        html_content = response.text
        og_image_url = None

        # 정규식 패턴을 사용하여 OG 이미지 URL 찾기
        og_image_pattern = r'<meta\s+property="og:image"\s+content="([^"]+)"\s*/?>'
        og_image_match = re.search(og_image_pattern, html_content)
        if og_image_match:
            og_image_url = og_image_match.group(1)
            print("OG 이미지 URL:", og_image_url)
        else:
            print("OG 이미지를 찾을 수 없습니다.")

        if image_type == "large":
            og_image_url = og_image_url.replace("_m.jpg", "_l.jpg")
        elif image_type == "small":
            og_image_url = og_image_url.replace("_m.jpg", "_s.jpg")

        return og_image_url

    @staticmethod
    def image_to_string(image_url, lang="kor"):
        """
        `KakaoTalkChannel.image_to_string` 이미지를 OCR을 통해 텍스트로 변경

        ## Example

        ```python
        from kakaotalkchannel import KakaoTalkChannel

        image_url = 'http://k.kakaocdn.net/xxxxx'
        image_text = KakaoTalkChannel.image_to_string(image_url)
        ```
        """

        if not image_url:
            return ""

        # 이미지 다운로드 및 열기
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # OCR을 통해 텍스트 추출
        text = pytesseract.image_to_string(image, lang=lang)

        # 추출된 텍스트 출력
        return text

    @staticmethod
    def send_slack(text):
        """
        `KakaoTalkChannel.send_slack` 이미지를 OCR을 통해 텍스트로 변경

        ## Example

        ```python
        from kakaotalkchannel import KakaoTalkChannel

        image_text = "slack send - image text"
        KakaoTalkChannel.send_slack(image_text)
        ```
        """

        response = requests.post(
            SLACK_SEND_URL,
            json={"text": text},
        )
        return response


if __name__ == "__main__":
    channel_url = "http://pf.kakao.com/_swtYxl"
    image_url = KakaoTalkChannel.get_profile_image(channel_url)
    image_text = KakaoTalkChannel.image_to_string(image_url)
    if image_text[0] == "0":
        image_text = image_text[1:]
    image_text += image_url
    print(image_text)
    r = KakaoTalkChannel.send_slack(image_text)
    print(SLACK_SEND_URL, r)
