import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AutoresPage } from './pages/authors/authors.component';
import { EditorasPage } from './pages/editoras/editoras.component';
import { LivrosPage } from './pages/livros/livros.component';
import { LoginComponent } from './pages/login.component/login.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'home', component: HomeComponent },
    { path: 'autores', component: AutoresPage },
    { path: 'editoras', component: EditorasPage },
    { path: 'livros', component: LivrosPage },
];
