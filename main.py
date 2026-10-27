from pathlib import Path

import cv2
import numpy as np


class ImagenExamen:

    def __init__(self, ruta):
        self.ruta = str(ruta)
        self.original = cv2.imread(self.ruta, cv2.IMREAD_COLOR)

        if self.original is None:
            raise ValueError(
                f"No se pudo cargar la imagen: {self.ruta}. "
                "Revisa la ruta y el formato."
            )

    def mostrar(self, titulo, imagen=None):
        if imagen is None:
            imagen = self.original

        # WINDOW_NORMAL permite ajustar la ventana con el ratón.
        cv2.namedWindow(titulo, cv2.WINDOW_NORMAL)
        cv2.imshow(titulo, imagen)


class PreprocesadorExamen:

    def __init__(self, umbral=150):
        if not isinstance(umbral, int) or not 0 <= umbral <= 255:
            raise ValueError(
                "El umbral debe ser un entero entre 0 y 255."
            )

        self.umbral = umbral

    def a_grises(self, imagen_bgr):
        alto, ancho, _ = imagen_bgr.shape
        gris = np.zeros((alto, ancho), dtype=np.uint8)

        for y in range(alto):
            for x in range(ancho):
                b, g, r = map(int, imagen_bgr[y, x])

                gris[y, x] = round(
                    0.114 * b + 0.587 * g + 0.299 * r
                )

        return gris

    def binarizar(self, gris):
        alto, ancho = gris.shape
        binaria = np.zeros((alto, ancho), dtype=np.uint8)

        for y in range(alto):
            for x in range(ancho):
                binaria[y, x] = (
                    255 if gris[y, x] > self.umbral else 0
                )

        return binaria


if __name__ == "__main__":
    ruta = Path(__file__).resolve().parent / "examen.jpg"

    examen = ImagenExamen(ruta)
    procesador = PreprocesadorExamen(umbral=150)

    imagen_gris = procesador.a_grises(examen.original)
    imagen_binaria = procesador.binarizar(imagen_gris)

    examen.mostrar("1 - Examen original")
    examen.mostrar("2 - Escala de grises", imagen_gris)
    examen.mostrar("3 - Imagen binaria", imagen_binaria)

    print("Preprocesamiento terminado.")
    print(f"Umbral utilizado: {procesador.umbral}")
    print("Presiona una tecla dentro de una ventana para cerrar.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()