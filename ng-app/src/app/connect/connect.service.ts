import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APP_CONFIG, IAppConfig } from '@app/core/core.config';
import { Observable } from 'rxjs';
import { Template } from './templates/template.models';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ConnectService {

  constructor(
    private http: HttpClient,
    @Inject(APP_CONFIG) private config: IAppConfig,
  ) { }

  getTemplates(): Observable<Template[]> {
    return this.http.get(this.config.apiEndpoint + '/templates')
      .pipe(map((response: Template[]) => response
      ));
  }
}
