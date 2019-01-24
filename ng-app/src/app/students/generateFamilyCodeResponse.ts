export interface Additionaldetail {
    studentid: string;
    fname: string;
    lname: string;
    paymentcode: string;
    dob: string;
    selected: boolean;
}

export interface GenerateFamilyCodeRes {
    status: number;
    sibWOPC : Additionaldetail[];
    sibWPC : Additionaldetail[];
    message: string;
}

export class GenerateFamilyCodeReq {
    constructor(private studentids: string[], private ignoresibligs: boolean, private basedon: string  ){}
}