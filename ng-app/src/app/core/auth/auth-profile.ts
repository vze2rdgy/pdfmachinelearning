export interface Loc {
    address: string;
    locationid: number;
    locationname: string;
}

export class AuthProfile {
    token: Token;
    userinfo: Userinfo;
    locids: number[];
    locs: Loc[];    
}

export interface Token {
    access_token: string;
    expires_at: number;
    expires_in: number;
    id_token: string;
    scope: string;
    token_type: string;
}

export interface Userinfo {
    at_hash: string;
    aud: string;
    azp: string;
    email: string;
    email_verified: boolean;
    exp: number;
    family_name: string;
    given_name: string;
    iat: number;
    iss: string;
    locale: string;
    name: string;
    nonce: string;
    picture: string;
    sub: string;
}


