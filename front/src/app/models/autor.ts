import { Observable } from "rxjs";
import { environnment } from "../environments/envoirnments";

export interface Autor {
    id: number;
    nome: string;
    sobrenome: string;
    data_nascimento?: string | null;  // se não existir, guarda null
    nacao?:string | null; 
    bio?: string | null; 
}