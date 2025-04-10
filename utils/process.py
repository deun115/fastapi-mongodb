import os
import cv2
from db.models import ProgressRequestObj
from db.collections import progress_cache_collection


def generate_url(path):
    endpoint = path.split('/')[:-2]
    url = "http://localhost:8000/" + endpoint
    return url


def execute_progress(progress: ProgressRequestObj):
    action = progress.action
    img_path = progress.initial_path

    try:
        # 이미지 불러오기 (BGR 형식)
        if os.path.exists(img_path):
            image = cv2.imread(img_path)

        if image is None:
            raise ValueError("이미지를 불러올 수 없습니다.")

        if action == "patch":
            # 예시: 좌상단 100x100 패치
            image = image[0:100, 0:100]

        elif action == "inverse_color":
            # 색 반전 (255 - 픽셀 값)
            image = 255 - image

        elif action == "rotate":
            # 예시: 90도 회전 (시계 방향)
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

        elif action == "resize":
            # 예시: 256x256 사이즈로 리사이즈
            image = cv2.resize(image, (256, 256))

        # 결과 저장
        new_path = os.path.splitext(img_path)[0] + f"_{action}.png"
        cv2.imwrite(new_path, image)

    except Exception as e:
        print("Fail to execute")
        result = None

    if result:
        status = "completed"
        output_url = generate_url(new_path)
    else:
        status = "error"
        output_url = ""

    output = {
        "name": progress.name,
        "action": progress.action,
        "status": status,
        "url": output_url
    }
    return output


async def save_execute_result(result):
    await progress_cache_collection.update_one(
        {"name": result["name"]},
        {"$set": result}
    )
    return True