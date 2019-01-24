import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CenterLocation } from './center-location';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  constructor(private http: HttpClient) { }

  registerLocation(locationdetails: CenterLocation): Observable<any>{
    return this.http.post("/api/register", locationdetails)
    .pipe( map( (response: any) => {
      console.log("response from register api = [" + JSON.stringify(response) +"]");
      return response;      
    } ));
  }
}
