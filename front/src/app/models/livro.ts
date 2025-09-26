export interface Livro {
    id: number;
    titulo: string;
    subtitulo?: string | null;
    autorId: number;
    editoraId: number;
    isbn?: string | null;
    descricao?: string | null;
    paginas?: number | null;
    ano?: number | null;
    preco?: number | null;
    estoque?: number | null;
    desconto?: number | null;
    disponivel?: string | null;
    dimensoes?: string | null;
    peso?: number | null;
    idioma?: string | null;
}