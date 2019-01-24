import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, flatMap, catchError } from 'rxjs/operators';
import { Setting } from '@app/shared/models/setting';
import { APP_CONFIG, IAppConfig } from '@app/core/core.config';
import { Store } from '@ngrx/store';
import { AppState } from '@app/core';
import { BaseResponse } from '@app/shared';
import { Address } from '@app/shared/models/address';
import { LocationMetadata } from '@app/shared/models/location';



@Injectable({
    providedIn: 'root'
})
export class SettingsService {
    private selectedLocId: number;
    // locid = this.authService.selectedLoction.locationid;
    setting: Setting[];

    constructor(
        private http: HttpClient,
        @Inject(APP_CONFIG) private config: IAppConfig,
        private store: Store<AppState>,
    ) { }

    GetSetting(locationID): Observable<Setting[]> {
        return this.http.get(this.config.apiEndpoint + "/settings/" + locationID)
            .pipe(map((response: Setting[]) => response
            ));
    }

    UpdateAddress(address: Address, locationID: number): Observable<BaseResponse> {
        var obj = address.toSettings();
        return this.UpdateSettings(obj, locationID);
    }

    UpdateFee() {
    }

    UpdateLocationDetails(location: LocationMetadata, locationID: number): Observable<BaseResponse> {
        var obj = location.toSettings();
        return this.UpdateSettings(obj, locationID);
    }

    UpdateSettings(obj, locationID: number): Observable<BaseResponse> {
        console.log(this.config.apiEndpoint);

        return this.http
            .post(this.config.apiEndpoint + "/settings/" + locationID, obj)
            .pipe(
                map((response: BaseResponse) => response
                ));
    }
}
