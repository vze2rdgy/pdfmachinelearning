import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, take } from 'rxjs/operators';
import { AuthService } from 'src/app/services/auth.service';
import { UploadResponse } from './upload-response';
import { APP_CONFIG, IAppConfig } from '@app/core/core.config';
import { Store } from '@ngrx/store';
import { AppState, selectCurrentLocation } from '@app/core';
import { Loc } from '@app/core/auth/auth-profile';

@Injectable({
  providedIn: 'root'
})
export class FileuploadService {

  private selectedLocId: number;
  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: HttpClient,
    private store: Store<AppState>,
  ) {
    this.store.select(selectCurrentLocation)
      .subscribe((currentlocation) => {
        if (currentlocation != null) {
          this.selectedLocId = currentlocation.locationid
        } else {
          // TODO: temp
          this.selectedLocId = 1
        }

      })
  }

  uploadFile(file: File, mapping: string, type): Observable<any> {

    console.log("current lcoation is =>" + this.selectedLocId);

    var formData = new FormData();
    formData.append("file", file);
    if (mapping != null) {
      formData.append("mapping", mapping);
    }
    return this.http.post(this.config.apiEndpoint + "/upload/" + this.selectedLocId + "/" + type, formData)
      .pipe(map((response: UploadResponse) => {
        console.log(response);
        return response;
      }));
  }
}
