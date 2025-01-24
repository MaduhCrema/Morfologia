from PIL import Image
import matplotlib.pyplot as plt

def read_image(path):
    # Lê a imagem e converte para tons de cinza
    img = Image.open(path).convert('L')

    # Converte para binário
    threshold = 128
    binary_img = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            row.append(1 if pixel > threshold else 0)
        binary_img.append(row)

    return binary_img

def erosion(binary_image, structuring_element):
    # Pega as dimensões da imagem e do elemento estruturante
    img_height, img_width = len(binary_image), len(binary_image[0])
    se_height, se_width = len(structuring_element), len(structuring_element[0])

    # Deslocamento do operador
    se_center_y, se_center_x = se_height // 2, se_width // 2

    # Matriz erodida (inicialmente preenchida com zeros)
    eroded_image = [[0 for _ in range(img_width)] for _ in range(img_height)]

    for y in range(se_center_y, img_height - se_center_y):
        for x in range(se_center_x, img_width - se_center_x):
            match = True
            for se_y in range(se_height):
                for se_x in range(se_width):
                    img_y = y + se_y - se_center_y
                    img_x = x + se_x - se_center_x
                    if structuring_element[se_y][se_x] == 1 and binary_image[img_y][img_x] != 1:
                        match = False
                        break
                if not match:
                    break
            if match:
                eroded_image[y][x] = 1

    return eroded_image

def dilation(binary_image, structuring_element):
    # Pega as dimensões da imagem e do elemento estruturante
    img_height, img_width = len(binary_image), len(binary_image[0])
    se_height, se_width = len(structuring_element), len(structuring_element[0])

    # Deslocamento do operador
    se_center_y, se_center_x = se_height // 2, se_width // 2

    # Matriz dilatada (inicialmente preenchida com zeros)
    dilated_image = [[0 for _ in range(img_width)] for _ in range(img_height)]

    for y in range(se_center_y, img_height - se_center_y):
        for x in range(se_center_x, img_width - se_center_x):
            match = False
            for se_y in range(se_height):
                for se_x in range(se_width):
                    img_y = y + se_y - se_center_y
                    img_x = x + se_x - se_center_x
                    if structuring_element[se_y][se_x] == 1 and binary_image[img_y][img_x] == 1:
                        match = True
                        break
                if match:
                    break
            if match:
                dilated_image[y][x] = 1

    return dilated_image

def save_image(binary_image, output_path):
    height = len(binary_image)
    width = len(binary_image[0])
    img = Image.new('L', (width, height))

    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), 255 if binary_image[y][x] == 1 else 0)

    img.save(output_path)

if __name__ == "__main__":
    input_path = "./bolinhas.png" #  coloque o caminho conforme os diretórios do seu computador
    output_path_eroded = "imagem_erodida.png"
    output_path_dilated = "imagem_dilatada.png"

    binary_img = read_image(input_path)

    # Operador estruturante
    structuring_element = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]

    eroded_img = erosion(binary_img, structuring_element)
    dilated_img = dilation(binary_img, structuring_element)

    save_image(eroded_img, output_path_eroded)
    save_image(dilated_img, output_path_dilated)

    # Plota as imagens
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.title("Imagem Original")
    plt.imshow(binary_img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Imagem Erodida")
    plt.imshow(eroded_img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("Imagem Dilatada")
    plt.imshow(dilated_img, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    print(f"Imagem erodida salva em: {output_path_eroded}")
    print(f"Imagem dilatada salva em: {output_path_dilated}")
