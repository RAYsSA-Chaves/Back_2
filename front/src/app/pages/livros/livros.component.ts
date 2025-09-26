import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LivrosServices } from '../../services/livros.services';
import { EditorasServices } from '../../services/editoras.services';
import { AutoresServices } from '../../services/autores.services';
import { Livro } from '../../models/livro';
import { Editora } from '../../models/editora';
import { Autor } from '../../models/autor';
import { AuthService } from '../../services/auth.services';
import { forkJoin } from 'rxjs';  // permite executar vários Observables em paralelo e aguardar todos finalizarem para retornar os resultados juntos

@Component({
  standalone: true,
  imports: [RouterLink],
  template: `
    <section style="max-width:900px;margin:2rem auto;padding:0 1rem">
      <h1>Livros</h1>

      @if (carregando()) {
        <p>Carregando…</p>
      } @else if (erro()) {
        <p style="color:#c62828">{{ erro() }}</p>
      } @else {
        <ul style="padding-left:1.25rem">
          @for (a of livros(); track a.id) {
            <li style="margin:.25rem 0">
              <strong>{{ a.titulo }} {{ "-" }} {{ a.subtitulo }}</strong>
              @if (a.autor) {
                — <em style="color:#666">{{ getNomeAutor(a.autor) }}</em>
              }
              @if (a.editora) {
                — <em style="color:#666">{{ getNomeEditora(a.editora) }}</em>
              }
              @if (a.isbn) { • {{ a.isbn }} }
              @if (a.descricao) { • {{ a.descricao }} }
              @if (a.paginas) { • {{ a.paginas }} }
              @if (a.ano) { • {{ a.ano }} }
              @if (a.preco) { • {{ a.preco }} }
              @if (a.estoque) { • {{ a.estoque }} }
              @if (a.desconto) { • {{ a.desconto }} }
              @if (a.disponivel) { • {{ a.disponivel }} }
              @if (a.dimensoes) { • {{ a.dimensoes }} }
              @if (a.peso) { • {{ a.peso }} }
              @if (a.idioma) { • {{ a.idioma }} }
            </li>
          }
        </ul>
      }

      <nav style="margin-top:1rem">
        <a routerLink="/">Voltar ao início</a>
      </nav>
    </section>
  `
})
export class LivrosPage {
  private svc = inject(LivrosServices); // serviço que puxa livros
  private editorasSvc = inject(EditorasServices); // serviço que puxa editoras
  private autoresSvc = inject(AutoresServices); // serviço que puxa autores
  private auth = inject(AuthService);   // autenticação/token

  // listas que serão carregadas do backend (guarda o que o serviço puxa)
  livros = signal<Livro[]>([]);
  autores = signal<Autor[]>([]);
  editoras = signal<Editora[]>([]);

  // controla o estado de "carregando..." na interface
  carregando = signal(true);
  // guarda uma mensagem de erro, caso algo dê errado
  erro = signal<string | null>(null);

  constructor() {
    // Mostra o token de autenticação no console
    console.log("Token de acesso: ", this.auth.token());
    // Ativa o carregamento
    this.carregando.set(true);
    
    // Faz requisições paralelas
    forkJoin({
      livros: this.svc.listar(),
      editoras: this.editorasSvc.listar(),
      autores: this.autoresSvc.listar()
    }).subscribe({  
      // Atualiza os signals com os dados retornados
      next: ({ livros, editoras, autores }) => {
        this.livros.set(livros);
        this.editoras.set(editoras);
        this.autores.set(autores);
        this.carregando.set(false); // desativa o carregamento
      },
      error: () => {
        this.erro.set('Falha ao carregar livros'); // define mensagem de erro
        this.carregando.set(false); // desativa o carregamento
      }
    });
  }

  // Pegar valores das foreign keys
  getNomeEditora(id: number): string {
    const editora = this.editoras().find(e => e.id === id);
    return editora ? editora.editora : 'Não informada';
  }
  getNomeAutor(id: number): string {
    const autor = this.autores().find(a => a.id === id);
    return autor ? autor.nome : 'Não informado';
  }
}
