SUMMARY = "Detector de emociones con TensorFlow Lite"
LICENSE = "CLOSED"

SRC_URI = "file://emodetec"

S = "${WORKDIR}"

do_install() {
    # Solo crear el directorio que realmente usas
    install -d ${D}${datadir}/emodetec
    
    # Copiar toda la carpeta emotion_app
    cp -r ${WORKDIR}/source/* ${D}${datadir}/emodetec/
    
    # Hacer ejecutable el script principal
    chmod +x ${D}${datadir}/emodetec/modelo_optimo.py
}

FILES:${PN} += "${datadir}/emodetec"
