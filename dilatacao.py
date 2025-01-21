import cv2
import numpy as np
import matplotlib.pyplot as plt

def dilatacao(image, elemento_estruturante):
    altura_imagem, largura_imagem = image.shape
    altura_elemento_estruturante, largura_elemento_estruturante = elemento_estruturante.shape
    altura_modificacao, largura_modificacao = altura_elemento_estruturante // 2, largura_elemento_estruturante // 2
    imagem_modificada = np.pad(image, ((altura_modificacao, altura_modificacao), (largura_modificacao, largura_modificacao)), mode='constant', constant_values=0)
    saida = np.zeros_like(image)


    for i in range(altura_imagem):
        for j in range(largura_imagem):
            regiao = imagem_modificada[i:i + altura_elemento_estruturante, j:j + largura_elemento_estruturante]
            if np.any(regiao * elemento_estruturante):
                saida[i, j] = 255

    return saida

caminho_imagem = "C:\Users\marco\Downloads\trabpid\Morfologia\imgs_erosao\bolinhas.png"  
cor_imagem = cv2.imread(caminho_imagem)  
image = cv2.cvtColor(cor_imagem, cv2.COLOR_BGR2GRAY)  
_, imagem_binaria = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
elemento_estruturante = np.ones((4, 4), dtype=np.uint8) 
imagem_dilatada = dilatacao(imagem_binaria, elemento_estruturante)
dilatacao_cv = cv2.dilate(imagem_binaria, elemento_estruturante, iterations=1)
fig, axis = plt.subplots(1, 5, figsize=(15, 5))

axis[0].imshow(cv2.cvtColor(cor_imagem, cv2.COLOR_BGR2RGB))
axis[0].set_title("Original")
axis[0].axis('off')

axis[1].imshow(image, cmap='gray')
axis[1].set_title("Acizentada")
axis[1].axis('off')

axis[2].imshow(imagem_binaria, cmap='gray')
axis[2].set_title("Imagem Binária")
axis[2].axis('off')

axis[3].imshow(imagem_dilatada, cmap='gray')
axis[3].set_title("Imagem Dilatada")
axis[3].axis('off')

axis[4].imshow(dilatacao_cv, cmap='gray')
axis[4].set_title("Dilatação OpenCV")
axis[4].axis('off')

plt.tight_layout()
plt.show()
