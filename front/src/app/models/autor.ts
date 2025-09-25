export interface Autor {
    id: number;
    nome: string;
    sobrenome?: string | null;
    data_nascimento?: string | null;
    nacao?: string | null;
    bio?: string | null;
}