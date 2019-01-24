import { Injectable, Inject } from '@angular/core';
import { StudentBasicInfo } from './home/home.model';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { APP_CONFIG, IAppConfig } from '@app/core/core.config';
import { map } from 'rxjs/operators';
import { Tuition } from './tuitions/tuitions.model';
import { GenerateFamilyCodeRes } from './generateFamilyCodeResponse';
import { BaseResponse } from '@app/shared';

@Injectable({
  providedIn: 'root'
})
export class StudentsService {

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private httpClient: HttpClient,
  ) { }


  getStudentBasicInfo(): Observable<StudentBasicInfo[]> {
    return this.httpClient
      .get(this.config.apiEndpoint + "/students")
      .pipe(
        map((response: StudentBasicInfo[]) => response
        ));
  }

  getTuitions(): Observable<Tuition[]> {
    return this.httpClient
      .get(this.config.apiEndpoint + "/tuitions")
      .pipe(
        map((response: Tuition[]) => response
        ));
  }

  generateFamilyCode(req): Observable<GenerateFamilyCodeRes> {
    console.log("generateFamilyCode" + JSON.stringify(req));

    return this.httpClient
      .post(this.config.apiEndpoint + "/gprn", req)
      .pipe(
        map((response: GenerateFamilyCodeRes) => response
        ));

    // return this.httpClient.post(this.config.apiEndpoint + "/gprn", req)
    //   .pipe(map((response: GenerateFamilyCodeRes) => {
    //     console.log("GenerateFamilyCodeRes : [ " + JSON.stringify(response) + " ]");
    //     return response;
    //   },
    //     error => {
    //       console.log("Unable to generate the family code " + JSON.stringify(error));
    //     }
    //   ));
  }

  UpdateTuitions(data): Observable<BaseResponse> {

    return this.httpClient
      .post(this.config.apiEndpoint + "/tuitions", data)
      .pipe(
        map((response: BaseResponse) => response
        ));
  }
}
