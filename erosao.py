from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def read_image(path):
    img = Image.open(path).convert('L')
    
    #converte pra binário 
    threshold = 128
    binary_img = np.array(img) > threshold

    return binary_img.astype(int)

def erosion(binary_image, structuring_element):
    # pega as dimensoes da imagem 
    img_height, img_width = binary_image.shape
    se_height, se_width = structuring_element.shape

    # deslocamento do operador
    se_center_y, se_center_x = se_height // 2, se_width // 2

    # matriz
    eroded_image = np.zeros_like(binary_image)

    for y in range(se_center_y, img_height - se_center_y):
        for x in range(se_center_x, img_width - se_center_x):
            region = binary_image[y - se_center_y:y + se_center_y + 1, x - se_center_x:x + se_center_x + 1]
            
            #verifica se o operador cabe na regiao do objeto da imagem
            if np.array_equal(region & structuring_element, structuring_element):
                eroded_image[y, x] = 1

    return eroded_image

def save_image(binary_image, output_path):
    img = Image.fromarray((binary_image * 255).astype(np.uint8))
    img.save(output_path)


if __name__ == "__main__":
    input_path = "./imgs_erosao/bolinhas.png"
    output_path = "imagem_erodida.png"

    binary_img = read_image(input_path)

    # operador
    structuring_element = np.array([[1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1]])

    eroded_img = erosion(binary_img, structuring_element)

    save_image(eroded_img, output_path)


    # plota as imagens
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Imagem Original")
    plt.imshow(binary_img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Imagem Erodida")
    plt.imshow(eroded_img, cmap="gray")
    plt.axis("off")


    plt.tight_layout()
    plt.show()

    print(f"Imagem erodida salva em: {output_path}")

