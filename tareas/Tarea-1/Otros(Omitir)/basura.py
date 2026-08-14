# for i in range(9):
#     imgInput = plt.imread(f"Kodak-Lossless-True-Color-Image-Suite/PhotoCD_PCD0992/0{i+1}.png").astype(float)
#     print(f"0{i+1}: {imgInput.shape}") 


# for i in range(10):
#     imgInput = plt.imread(f"Kodak-Lossless-True-Color-Image-Suite/PhotoCD_PCD0992/1{i}.png").astype(float)
#     print(f"1{i}: {imgInput.shape}") 

# for i in range(5):
#     imgInput = plt.imread(f"Kodak-Lossless-True-Color-Image-Suite/PhotoCD_PCD0992/2{i}.png").astype(float)
#     print(f"2{i}: {imgInput.shape}") 

def BilinearInterpolation(Y,RedMask,GreenMask,BlueMask):
    TRed   = np.array((RedMask   * Y), dtype=float)
    TGreen = np.array((GreenMask * Y), dtype=float)
    TBlue  = np.array((BlueMask  * Y), dtype=float)

    rows = TGreen.shape[0]
    columns = TGreen.shape[1]

    for i in range(rows):
        for j in range(columns):
            if GreenMask[i][j] == 0: # Recorremos la matriz verde
                #Manejar esquinas
                if i == 0 and j == 0:
                    TGreen[i][j] = 1/2 * (TGreen[i+1][j] + TGreen[i][j+1])
                elif i == 0 and j == columns -1:
                    TGreen[i][j] = 1/2 * (TGreen[i+1][j] + TGreen[i][j-1])
                elif i == (rows - 1) and j == 0:
                    TGreen[i][j] = 1/2 * (TGreen[i][j+1] + TGreen[i-1][j])
                elif i == (rows - 1) and j == (columns - 1):
                    TGreen[i][j] = 1/2 * (TGreen[i][j-1] + TGreen[i-1][j])
                #Manejar bordes    
                elif i == 0:
                    TGreen[i][j] = 1/3 * (TGreen[i][j-1]  + TGreen[i+1][j]  + TGreen[i][j+1])
                elif i == rows - 1:
                    TGreen[i][j] = 1/3 * (TGreen[i][j-1]  + TGreen[i-1][j]  + TGreen[i][j+1])
                elif j == 0:
                    TGreen[i][j] = 1/3 * (TGreen[i-1][j]  + TGreen[i][j+1]  + TGreen[i+1][j])
                elif j == columns - 1:
                    TGreen[i][j] = 1/3 * (TGreen[i-1][j]  + TGreen[i][j-1]  + TGreen[i+1][j])
                #Manejar general 
                else:
                    TGreen[i][j] = 1/4 * (TGreen[i+1][j]  + TGreen[i-1][j]  + TGreen[i][j+1] + TGreen[i][j-1])

            if RedMask[i][j] == 0: # Recorremos la matriz roja
                if BlueMask[i][j] == 0: #Posicion verde
                    #Casos de borde
                    if j == (columns - 1) and j%2 == 1:
                        TRed[i][j] = TRed[i][j-1]
                    elif i == (rows - 1)  and i%2 == 1:
                        TRed[i][j] = TRed[i-1][j]
                    #Manejar General
                    else:
                        if i%2 == 0:
                            TRed[i][j] = 1/2 * (TRed[i][j-1] + TRed[i][j+1])
                        else:
                            TRed[i][j] = 1/2 * (TRed[i-1][j] + TRed[i+1][j])
                        
                else:                 #Posicion azul
                    #Casos de borde
                    if i == (rows - 1) and j == (columns -1):
                        TRed[i][j] = TRed[i-1][j-1] 
                    elif j == (columns - 1):
                        TRed[i][j] = 1/2 * (TRed[i-1][j-1] + TRed[i+1][j-1])
                    elif i == (rows - 1):
                        TRed[i][j] = 1/2 * (TRed[i-1][j-1] + TRed[i-1][j+1])
                    #Manejar general 
                    else:
                        TRed[i][j] = 1/2 * (TRed[i-1][j-1] + TRed[i+1][j+1])

            if BlueMask[i][j] == 0: # Recorremos la matriz azul
                if RedMask[i][j] == 0: #Posicion verde
                    if j == 0:
                        TBlue[i][j] = TBlue[i][j+1]
                    elif i == 0:
                        TBlue[i][j] = TBlue[i+1][j]
                    #Manejar general 
                    else:
                        if i%2 == 0:
                            TBlue[i][j] = 1/2 * (TBlue[i-1][j] + TBlue[i+1][j])
                        else:
                            TBlue[i][j] = 1/2 * (TBlue[i][j-1] + TBlue[i][j+1])

                else:                 #Posicion Roja
                    #Casos de borde
                    if i == 0 and j == 0:
                        TBlue[i][j] = TBlue[i+1][j+1]
                    elif j == 0:
                        TBlue[i][j] = 1/2 * (TBlue[i-1][j+1] + TBlue[i+1][j+1])
                    elif i == 0:
                        TBlue[i][j] = 1/2 * (TBlue[i+1][j-1] + TBlue[i+1][j+1])
                    #Manejar general 
                    else:
                        TBlue[i][j] = 1/2 * (TBlue[i-1][j-1] + TBlue[i+1][j+1])

    Img= np.zeros((rows, columns, 3), dtype=float) #Imagen Reconstruida
    Img[:,:,0] = TRed
    Img[:,:,1] = TGreen
    Img[:,:,2] = TBlue 
    return Img
