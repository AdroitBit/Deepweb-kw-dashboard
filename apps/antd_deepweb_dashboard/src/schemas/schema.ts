export interface DeepWebInfo {
    keyword: string;
    url: string;
}

export interface DeepWebSuggest {
    url: string;
}

export interface PushKeyword {
    keyword: string;
}

export interface ServerHealth {
    cpu_percent: number;
    memory_percent: number;
}