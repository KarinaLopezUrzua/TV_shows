from src import app
from src.controladores import controlador_usuarios, controlador_otros

app.secret_key = 'mantener en secreto'

if __name__=="__main__":
    app.run(debug=True)  