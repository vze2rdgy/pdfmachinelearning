import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { SESSION_STORAGE, StorageService } from 'angular-webstorage-service'
import { Inject } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { AuthProfile, Loc } from './auth-profile';
import { IAppConfig, APP_CONFIG } from '../core.config';


const STORAGE_KEY = 'authProfile';

@Injectable({
  providedIn: 'root'
})
export class AuthService {


  authProfile: AuthProfile = null;
  selectedLoction: Loc = null;

  // User is called registeredUser only if there is a location associated with user
  isRegisteredUser = false;

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private httpClient: HttpClient,
    private cookieService: CookieService,
    private router: Router
  ) { }

  getAuthProfile(): Observable<AuthProfile> {
    return this.httpClient
      .get(this.config.apiEndpoint + "/getuserprofile")
      .pipe(
        map((response: AuthProfile) => response
        ));
  }

  clearAuthSession() {
    // delete the token
    // delete the stored profile
    // this.storage.remove(STORAGE_KEY);
    // delete the cookie
    this.isRegisteredUser = false;

    console.log("clearAuthSession 1");
    this.cookieService.deleteAll();
    return this.httpClient
      .get(this.config.apiEndpoint + "/logout")
      .pipe(map((response: boolean) => {
        console.log("clearAuthSession 2");
        this.authProfile = null
        return true;
      }));
  }

  public getLocationIds(): number[] {
    if (this.authProfile) {
      return this.authProfile.locids;
    }
    return null;
  }
  public getUserEmail() {
    if (this.authProfile && this.authProfile.userinfo) {
      return this.authProfile.userinfo.email;
    }
    return null;
  }
  public getUserName() {
    if (this.authProfile && this.authProfile.userinfo) {
      return this.authProfile.userinfo.given_name;
    }
    return null;
  }

  public getPicture() {
    if (this.authProfile && this.authProfile.userinfo) {
      return this.authProfile.userinfo.picture;
    }
    return null;
  }

}
