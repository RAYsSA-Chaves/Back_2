import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AutoresPage } from './pages/authors/authors.component';
import { EditorasPage } from './pages/editoras/editoras.component';
import { LivrosPage } from './pages/livros/livros.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'home', component: HomeComponent },
    { path: 'autores', component: AutoresPage },
    { path: 'editoras', component: EditorasPage },
    { path: 'livros', component: LivrosPage },
];
