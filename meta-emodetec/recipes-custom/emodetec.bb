SUMMARY = "Detector de emociones con TensorFlow Lite"
LICENSE = "CLOSED"

SRC_URI = "file://source"

S = "${WORKDIR}"

do_install() {
    # Solo crear el directorio que realmente usas
    install -d ${D}${datadir}/emodetect
    
    # Copiar toda la carpeta emotion_app
    cp -r ${WORKDIR}/source/* ${D}${datadir}/emodetect/
    
    # Hacer ejecutable el script principal
    chmod +x ${D}${datadir}/emodetect/modelo_optimo.py
}

FILES:${PN} += "${datadir}/emodetect"
