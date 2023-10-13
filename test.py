from google.cloud import vision

def detect_text(path):
    """Detects text in the file."""
    

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(f"Texts: {texts[0].description}")

    # for text in texts:
    #     print(f'\n"{text.description}"')

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

detect_text('test.jpg')