import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Autor } from "../models/autor";
import { environnment } from "../environments/envoirnments";

@Injectable({providedIn: 'root'})
export class AutoresService {
    private http = inject(HttpClient)
    private base = environnment.apiBase

    listar(): Observable<Autor[]>{
        const url = `${this.base}autores`
        return this.http.get<Autor[]>(url)
    }
}