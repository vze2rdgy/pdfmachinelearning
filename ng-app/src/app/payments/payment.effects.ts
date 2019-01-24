import { Injectable } from "@angular/core";
import { Actions, Effect, ofType } from "@ngrx/effects";
import { Action } from "@ngrx/store";
import { PaymentDetailsService } from "./payment-details.service";
import { ActionPaymentsRetrieve, PaymentsActionTypes, ActionPaymentsRetrieveSuccess, ActionPaymentsRetrieveError } from "./payment.actions";
import { switchMap, map, catchError } from "rxjs/operators";
import { of } from "rxjs";

@Injectable()
export class PaymentsEffects {
    constructor(
        private actions$: Actions<Action>,
        private service: PaymentDetailsService
    ) { }

    @Effect()
    retrievePaymentsInfo = this.actions$.pipe(
        ofType<ActionPaymentsRetrieve>(PaymentsActionTypes.RETRIEVE),
        switchMap((action: ActionPaymentsRetrieve) =>
            this.service.getPaymentDetails().pipe(
               map(paymentcodeInfo =>{
                    return new ActionPaymentsRetrieveSuccess({payments: paymentcodeInfo});
               }),
               catchError( error => {
                   return of(new ActionPaymentsRetrieveError({error: error}));
               })
            )
        )
    );
}