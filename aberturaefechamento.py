from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def read_image(path):
    img = Image.open(path).convert('L')
    threshold = 128
    binary_img = np.array(img) > threshold
    return binary_img.astype(int)

def save_image(binary_image, output_path):
    img = Image.fromarray((binary_image * 255).astype(np.uint8))
    img.save(output_path)

def erosion(binary_image, structuring_element):
    img_height, img_width = binary_image.shape
    se_height, se_width = structuring_element.shape
    se_center_y, se_center_x = se_height // 2, se_width // 2
    eroded_image = np.zeros_like(binary_image)

    for y in range(se_center_y, img_height - se_center_y):
        for x in range(se_center_x, img_width - se_center_x):
            region = binary_image[y - se_center_y:y + se_center_y + 1, x - se_center_x:x + se_center_x + 1]
            if np.array_equal(region & structuring_element, structuring_element):
                eroded_image[y, x] = 1

    return eroded_image

def dilation(binary_image, structuring_element):
    img_height, img_width = binary_image.shape
    se_height, se_width = structuring_element.shape
    se_center_y, se_center_x = se_height // 2, se_width // 2
    dilated_image = np.zeros_like(binary_image)

    for y in range(se_center_y, img_height - se_center_y):
        for x in range(se_center_x, img_width - se_center_x):
            region = binary_image[y - se_center_y:y + se_center_y + 1, x - se_center_x:x + se_center_x + 1]
            if np.any(region & structuring_element):
                dilated_image[y, x] = 1

    return dilated_image

def opening(binary_image, structuring_element):
    eroded = erosion(binary_image, structuring_element)
    opened = dilation(eroded, structuring_element)
    return opened

def closing(binary_image, structuring_element):
    dilated = dilation(binary_image, structuring_element)
    closed = erosion(dilated, structuring_element)
    return closed

if __name__ == "__main__":
    input_path = r"C:\Users\marco\Downloads\trabpid\Morfologia\imgs_erosao\bolinhas.png"
    output_opening_path = "imagem_abertura.png"
    output_closing_path = "imagem_fechamento.png"

    binary_img = read_image(input_path)

    structuring_element = np.array([[1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1]])


    opened_img = opening(binary_img, structuring_element)
    closed_img = closing(binary_img, structuring_element)

    save_image(opened_img, output_opening_path)
    save_image(closed_img, output_closing_path)

    # Exibir as imagens
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.title("Imagem Original")
    plt.imshow(binary_img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Imagem Abertura")
    plt.imshow(opened_img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("Imagem Fechamento")
    plt.imshow(closed_img, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    print(f"Imagem de abertura salva em: {output_opening_path}")
    print(f"Imagem de fechamento salva em: {output_closing_path}")