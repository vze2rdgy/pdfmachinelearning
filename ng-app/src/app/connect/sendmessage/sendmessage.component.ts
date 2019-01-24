import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { Template } from '../templates/template.models';

@Component({
  selector: 'lynx-sendmessage',
  templateUrl: './sendmessage.component.html',
  styleUrls: ['./sendmessage.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SendmessageComponent implements OnInit {
 
  @Input() selectedTemplate : Template = null;

  data = [{id : 1, image: '',  name : 'name 1' },
  {id : 2, image: '',  name : 'name 2' },
  {id : 3, image: '',  name : 'name 3' },
  {id : 4, image: '',  name : 'name 4' }
];

  constructor() { }

  ngOnInit() {
  }

}
