from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "sekretnyklucz"

ceny = {
    "drukarka": 2000,
    "filament": 100,
    "czesci": 300
}

@app.route("/", methods=["GET", "POST"])
def index():

    if "koszyk" not in session:
        session["koszyk"] = []

    cena_koncowa = None

    if request.method == "POST":

        produkt = request.form["produkt"]
        ilosc = int(request.form["ilosc"])

        cena = ceny[produkt] * ilosc

        if "gwarancja" in request.form:
            cena += 200

        if "dostawa" in request.form:
            cena += 50

        cena_koncowa = cena

        # dodanie produktu do koszyka
        koszyk = session["koszyk"]
        koszyk.append({
            "produkt": produkt,
            "ilosc": ilosc,
            "cena": cena
        })
        session["koszyk"] = koszyk

    suma = sum(item["cena"] for item in session["koszyk"])

    return render_template("index.html", cena=cena_koncowa, koszyk=session["koszyk"], suma=suma)


@app.route("/zamowienie", methods=["POST"])
def zamowienie():

    imie = request.form["imie"]
    email = request.form["email"]

    koszyk = session.get("koszyk", [])

    return render_template("zamowienie.html", imie=imie, email=email, koszyk=koszyk)

@app.route("/usun/<int:index>")
def usun(index):

    koszyk = session.get("koszyk", [])

    if 0 <= index < len(koszyk):
        koszyk.pop(index)

    session["koszyk"] = koszyk

    return redirect("/")

@app.route("/wyczysc")
def wyczysc():

    session["koszyk"] = []

    return redirect("/")    

if __name__ == "__main__":
    app.run(debug=True)