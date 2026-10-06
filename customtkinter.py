import customtkinter as ctk
from tkinter import messagebox


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GerenciadorTarefas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Tarefas")
        self.geometry("600x650")
        self.resizable(False, False)

        self.tarefas = []

        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Gerenciador de Tarefas",
            font=("Arial", 28, "bold")
        )
        self.titulo.pack(pady=(30, 10))

        # Subtítulo
        self.subtitulo = ctk.CTkLabel(
            self,
            text="Organize suas tarefas de forma simples",
            font=("Arial", 14)
        )
        self.subtitulo.pack(pady=(0, 25))

        # Campo para digitar tarefa
        self.entrada = ctk.CTkEntry(
            self,
            placeholder_text="Digite uma tarefa...",
            width=400,
            height=45
        )
        self.entrada.pack(pady=10)

        # Botão adicionar
        self.botao_adicionar = ctk.CTkButton(
            self,
            text="Adicionar tarefa",
            width=200,
            height=40,
            command=self.adicionar_tarefa
        )
        self.botao_adicionar.pack(pady=10)

        # Área das tarefas
        self.lista = ctk.CTkScrollableFrame(
            self,
            width=500,
            height=350
        )
        self.lista.pack(pady=20)

    def adicionar_tarefa(self):
        texto = self.entrada.get().strip()

        if not texto:
            messagebox.showwarning(
                "Aviso",
                "Digite uma tarefa antes de adicionar."
            )
            return

        self.tarefas.append(texto)
        self.entrada.delete(0, "end")

        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        for i, tarefa in enumerate(self.tarefas):
            linha = ctk.CTkFrame(self.lista)
            linha.pack(fill="x", pady=5, padx=5)

            texto = ctk.CTkLabel(
                linha,
                text=tarefa,
                anchor="w",
                font=("Arial", 14)
            )
            texto.pack(
                side="left",
                padx=10,
                pady=10,
                expand=True,
                fill="x"
            )

            concluir = ctk.CTkButton(
                linha,
                text="✓",
                width=40,
                command=lambda indice=i: self.concluir_tarefa(indice)
            )
            concluir.pack(side="right", padx=3)

            excluir = ctk.CTkButton(
                linha,
                text="X",
                width=40,
                fg_color="#c0392b",
                hover_color="#922b21",
                command=lambda indice=i: self.excluir_tarefa(indice)
            )
            excluir.pack(side="right", padx=3)

    def concluir_tarefa(self, indice):
        tarefa = self.tarefas[indice]

        messagebox.showinfo(
            "Tarefa concluída",
            f"Você concluiu:\n\n{tarefa}"
        )

        self.tarefas.pop(indice)
        self.atualizar_lista()

    def excluir_tarefa(self, indice):
        self.tarefas.pop(indice)
        self.atualizar_lista()


if __name__ == "__main__":
    app = GerenciadorTarefas()
    app.mainloop()