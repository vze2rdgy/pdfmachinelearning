import { Setting } from "./setting";

export class LocationMetadata {

    public LocationName: string;
    public Phone1: string;
    public Phone2: string;
    public ReadingFee: number;
    public MathFee: number;

    toSettings() :Setting[] {
        var obj : Setting[] =[];
        obj.push(new Setting("locationname",this.LocationName,1));
        obj.push(new Setting("phone1",this.Phone1,1));
        obj.push(new Setting("phone2",this.Phone2,1));
        obj.push(new Setting("readingfee",this.ReadingFee!.toString(),1));
        obj.push(new Setting("mathfee",this.MathFee!.toString(),1));
        return obj;
    }

    fromSettings(settings: Setting[]){
        var tempSettings
        if (settings.length > 0) {
          tempSettings = settings.filter(s => s.key == 'locationname')
          if (tempSettings.length > 0) {
            this.LocationName = tempSettings[0].value;
          }
  
          tempSettings = settings.filter(s => s.key == 'phone1')
          if (tempSettings.length > 0) {
            this.Phone1 = tempSettings[0].value;
          }
  
          tempSettings = settings.filter(s => s.key == 'phone2')
          if (tempSettings.length > 0) {
            this.Phone2 = tempSettings[0].value;
          }
          tempSettings = settings.filter(s => s.key == 'readingfee')
          if (tempSettings.length > 0) {
            this.ReadingFee = Number(tempSettings[0].value);
          }
          tempSettings = settings.filter(s => s.key == 'mathfee')
          if (tempSettings.length > 0) {
            this.MathFee = Number(tempSettings[0].value);
          }
        }
    }
}
