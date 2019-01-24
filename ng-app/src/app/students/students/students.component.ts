import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { routeAnimations, selectAuth } from '@app/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Store, select } from '@ngrx/store';
import { State } from '../student.state';
import { ActionStudentsRetrieve } from '../home/home.actions';

@Component({
  selector: 'lynx-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.scss'],
  animations: [routeAnimations],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class StudentsComponent implements OnInit {

  isAuthenticated$: Observable<boolean>;

  studentsMenu = [
    { link: 'home', label: 'lynx.students.menu.home' },
    { link: 'tuitions', label: 'lynx.students.menu.tuitions' },
    { link: 'upload', label: 'lynx.students.menu.upload' },
  ]

  constructor(private store: Store<State>) {}

  ngOnInit(): void {
    this.isAuthenticated$ = this.store.pipe(
      select(selectAuth),
      map(auth => auth.isAuthenticated)      
    );
  }
}
 