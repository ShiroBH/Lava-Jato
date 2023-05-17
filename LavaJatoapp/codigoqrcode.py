import qrcode


qr = qrcode.QRCode(
    version=40,
    error_correction=qrcode.ERROR_CORRECT_L,
    box_size= 10,
    border= 1
)

qrCPF = "variavel CPF recebido do formulario"

imgQR = qrcode.make(qr)

imgQR.save(f'Lavajatoapp/static/imgQRChave/{qrCPF}.png')