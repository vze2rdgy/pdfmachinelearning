import { Setting } from "./setting";

export class Address {

    public address1: string;
    public address2: string;
    public city: string;
    public zipcode: string;
    public state: string;
    public country: string

    // constructor(
    //     public address1: string,
    //     public address2: string,
    //     public city: string,
    //     public zipcode: string,
    //     public state: string,
    //     public country: string) 
    //     { }
    toSettings() :Setting[] {
        var obj : Setting[] =[];
        obj.push(new Setting("address1",this.address1,1));
        obj.push(new Setting("address2",this.address2,1));
        obj.push(new Setting("city",this.city,1));
        obj.push(new Setting("state",this.state,1));
        obj.push(new Setting("zipcode",this.zipcode,1));
        obj.push(new Setting("country",this.country,1));
        return obj;
    }
    fromSettings(settings: Setting[]){
        var tempSettings
        if (settings.length > 0) {
          tempSettings = settings.filter(s => s.key == 'address1')
          if (tempSettings.length > 0) {
            this.address1 = tempSettings[0].value
          }
  
          tempSettings = settings.filter(s => s.key == 'address2')
          if (tempSettings.length > 0) {
            this.address2 = tempSettings[0].value
          }
  
          tempSettings = settings.filter(s => s.key == 'city')
          if (tempSettings.length > 0) {
            this.city = tempSettings[0].value
          }
  
          tempSettings = settings.filter(s => s.key == 'state')
          if (tempSettings.length > 0) {
            this.state = tempSettings[0].value
          }
  
          tempSettings = settings.filter(s => s.key == 'zipcode')
          if (tempSettings.length > 0) {
            this.zipcode = tempSettings[0].value
          }
  
          tempSettings = settings.filter(s => s.key == 'country')
          if (tempSettings.length > 0) {
            this.country = tempSettings[0].value
          }
        }
    }

}


