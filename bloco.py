import tkinter as tk

# Mapeamento de substituição de números
substitution_map = {
    '0': '1',
    '1': '0',
    '2': '9',
    '3': '8',
    '4': '7',
    '5': '6',
    '6': '5',
    '7': '4',
    '8': '3',
    '9': '2'
}

def replace_numbers(text):
    return ''.join(substitution_map.get(char, char) for char in text)

def on_text_change(event):
    text = text_widget.get("1.0", "end-1c")
    result = replace_numbers(text)
    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", result)

# Configuração da janela
window = tk.Tk()
window.title("Bloco de Notas com Substituição de Números")

# Área de texto
text_widget = tk.Text(window, wrap=tk.WORD)
text_widget.pack(fill=tk.BOTH, expand=True)

# Vincule o evento de alteração de texto à função de substituição
text_widget.bind("<KeyRelease>", on_text_change)

# Iniciar a interface gráfica
window.mainloop()
