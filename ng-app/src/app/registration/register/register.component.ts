import { Component, OnInit, OnDestroy } from '@angular/core';


import { AuthProfile } from '../models/auth-profile';
import { Router } from '@angular/router';
import { CenterLocation } from '../center-location';
import { RegisterService } from '../register.service';
import { AuthService, ActionAuthLogout, NotificationService, ActionReqAuthorization } from '@app/core';
import { Store, select } from '@ngrx/store';
import { State } from '../registration.state';
import { ActionRegistrationRegister } from '../registration.actions';
import { selectRegistrationsState } from '../registration.selectors';
import { takeUntil } from 'rxjs/operators';
import { componentDestroyed } from '@w11k/ngx-componentdestroyed';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit, OnDestroy {
  step = 0;
  model: CenterLocation = new CenterLocation();
  userName = "";

  constructor(
    private service: RegisterService,
    private authService: AuthService,
    private router: Router,
    private store: Store<State>,
    private notificationService: NotificationService
  ) { }

  ngOnInit() {
    this.userName = this.authService.getUserName();
    console.log("Username  is [" + this.userName + "]");
    this.store.pipe(select(selectRegistrationsState))
      .pipe(
        takeUntil(componentDestroyed(this))
      )
      .subscribe(state => {
        if (state != null) {
          //registration failed
          if (state.error != null) {
            this.notificationService.error("Registration Failed");
          }
        }
      });
  }

  ngOnDestroy() {
  }
  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }

  onSubmit() {
    this.store.dispatch(new ActionRegistrationRegister({ location: this.model }));

    // console.log("hello onSubmit" + JSON.stringify(this.model) );
    // this.service.registerLocation(this.model).subscribe((response)=>{
    //   console.log ("ResisterComponent " + JSON.stringify(response));
    //   if (response.status = true){
    //     this.authService.refreshAuthProfile().subscribe((response:AuthProfile)=>{
    //       console.log("refreshed");
    //       this.router.navigateByUrl('/');
    //     });
    //   }else{
    //     console.log("response.status is false [ " + response.status +" ]" )
    //   }
    // });
  }
}
