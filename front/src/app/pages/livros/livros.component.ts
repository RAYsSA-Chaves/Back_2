import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LivrosServices } from '../../services/livros.services';
import { EditorasServices } from '../../services/editoras.services';
import { AutoresServices } from '../../services/autores.services';
import { Livro } from '../../models/livro';
import { Editora } from '../../models/editora';
import { Autor } from '../../models/autor';
import { AuthService } from '../../services/auth.services';
import { forkJoin } from 'rxjs';

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
              @if (a.autorId) {
                — <em>{{ getNomeAutor(a.autorId) }}</em>
              }
              @if (a.editoraId) {
                — <em>{{ getNomeEditora(a.editoraId) }}</em>
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
  private svc = inject(LivrosServices);
  private editorasSvc = inject(EditorasServices);
  private autoresSvc = inject(AutoresServices);
  private auth = inject(AuthService);   //Ver o token

  livros = signal<Livro[]>([]);
  autores = signal<Autor[]>([]);
  editoras = signal<Editora[]>([]);

  carregando = signal(true);
  erro = signal<string | null>(null);

  constructor() {
    console.log("Token de acesso: ", this.auth.token());

    this.carregando.set(true);
    
    forkJoin({
      livros: this.svc.listar(),
      editoras: this.editorasSvc.listar(),
      autores: this.autoresSvc.listar()
    }).subscribe({
      next: ({ livros, editoras, autores }) => {
        this.livros.set(livros);
        this.editoras.set(editoras);
        this.autores.set(autores);
        this.carregando.set(false);
      },
      error: () => {
        this.erro.set('Falha ao carregar livros');
        this.carregando.set(false);
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