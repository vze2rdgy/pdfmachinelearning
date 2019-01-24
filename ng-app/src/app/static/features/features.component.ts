import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';

import { ROUTE_ANIMATIONS_ELEMENTS } from '@app/core';

import { Feature, features } from './features.data';
import { Store } from '@ngrx/store';
import { State } from '@app/students/student.state';
import { ActionStudentsRetrieve } from '@app/students/home/home.actions';

@Component({
  selector: 'lynx-features',
  templateUrl: './features.component.html',
  styleUrls: ['./features.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturesComponent implements OnInit {
  routeAnimationsElements = ROUTE_ANIMATIONS_ELEMENTS;
  features: Feature[] = features;

  constructor(
    private store: Store<State>
  ) { }

  ngOnInit() {}

  openLink(link: string) {
    window.open(link, '_blank');
  }

  retStu(){
    this.store.dispatch(new ActionStudentsRetrieve({ timestamp: '10-10-219' }));
  }
}
