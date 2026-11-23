"""NASA Turbofan RUL: canlı demo (Gradio). Hugging Face Space'te çalışacak şekilde hazırlandı.

data/ klasöründe 12 dosya olmalı: train_FD001.txt, test_FD001.txt, RUL_FD001.txt ... FD004.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gradio as gr
from sklearn.ensemble import RandomForestRegressor

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
KOLONLAR = ["unit", "cycle"] + [f"setting_{i}" for i in range(1, 4)] + [f"sensor_{i}" for i in range(1, 22)]
KUMELER = ["FD001", "FD002", "FD003", "FD004"]
_CACHE = {}


def eksik_dosyalar():
    return [f"{p}_{ds}.txt" for ds in KUMELER for p in ("train", "test", "RUL")
            if not os.path.exists(os.path.join(DATA_DIR, f"{p}_{ds}.txt"))]


def yukle(ds):
    """Veriyi oku, ana defterlerdeki gibi hazırla ve modeli eğit (kümeye bir kez)."""
    if ds in _CACHE:
        return _CACHE[ds]
    tr = pd.read_csv(os.path.join(DATA_DIR, f"train_{ds}.txt"), sep=r"\s+", header=None, names=KOLONLAR)
    te = pd.read_csv(os.path.join(DATA_DIR, f"test_{ds}.txt"), sep=r"\s+", header=None, names=KOLONLAR)
    rul = pd.read_csv(os.path.join(DATA_DIR, f"RUL_{ds}.txt"), header=None, names=["RUL"])
    std = tr.std()
    sabit = std[std < 0.01].index
    tr, te = tr.drop(columns=sabit), te.drop(columns=sabit)
    tr["RUL"] = tr.groupby("unit")["cycle"].transform("max") - tr["cycle"]
    ozellikler = list(tr.columns.drop(["unit", "cycle", "RUL"]))
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(tr[ozellikler], tr["RUL"].clip(upper=125))
    _CACHE[ds] = dict(te=te, rul=rul, f=ozellikler, m=model, med=tr[ozellikler].median())
    return _CACHE[ds]


def motor_tahmini(ds, motor_no, cevrim, esik):
    d = yukle(ds)
    motor_no = int(motor_no)
    motor = d["te"][d["te"]["unit"] == motor_no].reset_index(drop=True)
    n = len(motor)
    cevrim = int(min(max(cevrim, 1), n))
    tahmin = d["m"].predict(motor.iloc[:cevrim][d["f"]])
    son_tahmin = float(tahmin[-1])
    son_gercek = int(d["rul"]["RUL"].iloc[motor_no - 1])
    gercek = np.minimum(125, son_gercek + (n - np.arange(1, cevrim + 1)))
    simdiki = int(gercek[-1])
    alarm, yakin = son_tahmin <= esik, simdiki <= 30
    durum = ("Doğru alarm" if alarm and yakin else "Yanlış alarm" if alarm else
             "Kaçırılan arıza" if yakin else "Doğru: alarm yok")
    fig, ax = plt.subplots(figsize=(7, 3.6))
    x = np.arange(1, cevrim + 1)
    ax.plot(x, tahmin, label="Tahmin (Random Forest)", color="tab:blue")
    ax.plot(x, gercek, label="Gerçek RUL (en çok 125)", color="gray", linestyle="--")
    ax.axhline(esik, color="tab:orange", linewidth=1, label="Alarm eşiği")
    ax.set_xlim(1, n)
    ax.set_xlabel("Çevrim")
    ax.set_ylabel("Kalan ömür (çevrim)")
    ax.legend()
    plt.close(fig)
    yazi = (f"**Tahmini kalan ömür:** {son_tahmin:.0f} çevrim  \n"
            f"**Gerçek kalan ömür (en çok 125):** {simdiki} çevrim  \n"
            f"**Durum:** {durum}")
    return fig, yazi


def motor_degisti(ds, motor_no):
    d = yukle(ds)
    n = int((d["te"]["unit"] == int(motor_no)).sum())
    return gr.update(maximum=n, value=n)


def kume_degisti(ds):
    d = yukle(ds)
    n_motor = int(d["te"]["unit"].nunique())
    n1 = int((d["te"]["unit"] == 1).sum())
    tablo = pd.DataFrame([d["med"].round(3).to_dict()])
    return (gr.update(maximum=n_motor, value=1), gr.update(maximum=n1, value=n1), tablo, "")


def sensor_tahmini(ds, tablo):
    d = yukle(ds)
    satir = pd.DataFrame(tablo).iloc[[0]][d["f"]].astype(float)
    return f"**Tahmini kalan ömür:** {float(d['m'].predict(satir)[0]):.0f} çevrim"


with gr.Blocks(title="Motor Ömrü Tahmini") as demo:
    gr.Markdown("# NASA Turbofan: Motor Ömrü Tahmini\nEğitilmiş Random Forest, kaydırıcıları her oynattığında **canlı** tahmin üretir. "
                "Küme değiştirince model o kümenin verisiyle yeniden eğitilir (birkaç saniye sürer).")
    eksik = eksik_dosyalar()
    if eksik:
        gr.Markdown("**Eksik veri dosyaları:** " + ", ".join(eksik) + "\n\nBunları Space'in `data/` klasörüne yükle.")
    ds_in = gr.Dropdown(KUMELER, value="FD001", label="Veri kümesi")
    with gr.Tab("Test motoru"):
        with gr.Row():
            motor_in = gr.Slider(1, 100, value=1, step=1, label="Motor numarası")
            cevrim_in = gr.Slider(1, 31, value=31, step=1, label="Şu anki çevrim")
            esik_in = gr.Slider(20, 60, value=40, step=5, label="Bakım uyarı eşiği (çevrim)")
        grafik = gr.Plot(label="Tahmin ve gerçek RUL")
        yazi = gr.Markdown()
        girdiler = [ds_in, motor_in, cevrim_in, esik_in]
        motor_in.change(motor_degisti, [ds_in, motor_in], cevrim_in)
        for g in (motor_in, cevrim_in, esik_in):
            g.change(motor_tahmini, girdiler, [grafik, yazi])
    with gr.Tab("Sensör değerlerini gir"):
        gr.Markdown("Tablodaki değerleri düzenle ve **Tahmin et**'e bas. Başlangıç değerleri eğitim verisinin medyanıdır. "
                    "Model yalnızca bu tek satıra bakar, motorun geçmişini bilmez.")
        tablo = gr.Dataframe(interactive=True, label="Sensör ve ayar değerleri")
        dugme = gr.Button("Tahmin et")
        sonuc = gr.Markdown()
        dugme.click(sensor_tahmini, [ds_in, tablo], sonuc)
    ds_in.change(kume_degisti, ds_in, [motor_in, cevrim_in, tablo, sonuc]).then(
        motor_tahmini, girdiler, [grafik, yazi])
    if not eksik:
        demo.load(kume_degisti, ds_in, [motor_in, cevrim_in, tablo, sonuc]).then(
            motor_tahmini, girdiler, [grafik, yazi])

if __name__ == "__main__":
    demo.launch()
