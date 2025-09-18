import { Injectable, signal } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environnment } from "../environments/envoirnments";

type TokenPair = {access: string; refresh?: string}

const storage = {
    get: (k: string) => (typeof localStorage !== 'undefined' ? localStorage.getItem(k) : null),
    set: (k: string, v: string) => {if (typeof localStorage !== 'undefined') localStorage.setItem(k, v)}
}