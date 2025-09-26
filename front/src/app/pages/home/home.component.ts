import { Component } from "@angular/core";
import { RouterLink } from "@angular/router";

@Component({
    selector:'app-home',
    standalone: true,
    imports: [RouterLink],
    template: `
    <section style="max-width:900px;margin:2rem auto;padding:0 1rem">
      <h1 style="margin:0 0 .75rem">Bem-vindo</h1>
      <p>Esta é a página inicial.</p>

      <nav style="margin-top:1rem; display:flex; gap:.75rem">
        <a routerLink="autores">Ver autores</a>
      </nav>
      <nav style="margin-top:1rem; display:flex; gap:.75rem">
        <a routerLink="editoras">Ver editoras</a>
      </nav>
      <nav style="margin-top:1rem; display:flex; gap:.75rem">
        <a routerLink="livros">Ver livros</a>
      </nav>
    </section>
  `
})

export class HomeComponent {}