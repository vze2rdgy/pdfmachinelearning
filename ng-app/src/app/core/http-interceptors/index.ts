/* "Barrel" of Http Interceptors; see HttpClient docs and sample code for more info */
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { HttpErrorInterceptor } from './http-error.interceptor';
import { MockBackendIntercepter } from './mock-backend-intercepter';

/** Http interceptor providers in outside-in order */
export const httpInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true }
];

export let mockupBackendProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: MockBackendIntercepter,
  multi: true
}