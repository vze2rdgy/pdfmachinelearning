import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { PaymentcodeInfo } from './payment.models';
import { APP_CONFIG, IAppConfig } from '@app/core/core.config';

@Injectable({
  providedIn: 'root'
})
export class PaymentDetailsService {
  constructor(
    private http: HttpClient,
    @Inject(APP_CONFIG) private config: IAppConfig,
  ) { }

  getPaymentDetails(): Observable<[PaymentcodeInfo]> {
    // TODO: return existing data if there is any     
    return this.http.get(this.config.apiEndpoint + '/paymentinfo/12/2018')
      .pipe(map((response: [PaymentcodeInfo]) => response
      ));
  }
}
