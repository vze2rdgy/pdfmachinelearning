export class Setting {
    key: string;
    value: string;
    group: number;
    constructor(key : string, value: string, group: number){
        this.key = key;
        this.value = value;
        this.group = group;
    }
}