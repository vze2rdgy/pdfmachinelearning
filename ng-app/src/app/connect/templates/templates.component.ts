import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  ViewChild,
  OnDestroy
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { State } from '../connect.state';
import { selectTemplates } from '../connect.selectors';
import { takeUntil } from 'rxjs/operators';
import { componentDestroyed } from '@w11k/ngx-componentdestroyed';
import { Template } from './template.models';



@Component({
  selector: 'lynx-templates',
  templateUrl: './templates.component.html',
  styleUrls: ['./templates.component.scss']
})
export class TemplatesComponent implements OnInit , OnDestroy{
  name = 'ng2-ckeditor';
  ckeConfig: any;
  mycontent: string;

  log = '';

  @ViewChild('myckeditor') ckeditor: any;

  isListVisible = false;
  isListItemSelected = false;
  templates: Template[] = [];
  selectedTemplate : Template
  isEditing = false;  
  isSend = false;

  templList = [
    { templateId: 'hh', templateName: 'Happy holiday' },
    { templateId: 'rm1', templateName: 'Reminder1' },
    { templateId: 'rm2', templateName: 'Closed due to weater' },
  ]

  listItemsFromDb = [
    { id: '[-Age-]', value: 'Age' },
    { id: '[-Address-]', value: 'Address' },
    { id: '[-firstname-]', value: 'firstname' },
    { id: '[-firstname-]', value: 'lastname' },
    { id: '[-firstname-]', value: 'City' }
  ];

  listItems = this.listItemsFromDb;
  nextChar = null;

  constructor(
    private route: ActivatedRoute,
    private store: Store<State>,
    private router: Router
  ) {

    this.mycontent = `<p>My html content</p>`;

  }

  ngOnInit() {

    this.route.data.subscribe(data => {
      console.log(data);
    });

    this.ckeConfig = {
      allowedContent: false,
      extraPlugins: 'divarea',
      forcePasteAsPlainText: true
    };

    this.store.select(selectTemplates).pipe(takeUntil(componentDestroyed(this)))
    .subscribe(templates => {
      this.templates = templates
      this.selectedTemplate = templates[0];
      this.mycontent = this.selectedTemplate.templateHtml;
    })

  }

  onChange($event: any): void {
    console.log("Asd");
    if (!this.isListItemSelected) {
      this.isListVisible =
        this.mycontent.includes('@@') || this.mycontent.includes('@@');
      const stringIndex = this.mycontent.indexOf('@@');
      if (stringIndex > -1 && stringIndex + 2 + 1 <= this.mycontent.length) {
        this.nextChar = this.mycontent.substr(stringIndex + 2, 1);
        const filteredItem = this.listItemsFromDb.filter(item => item.value.toLowerCase().startsWith(this.nextChar.toLowerCase(), 0));
        if (filteredItem && filteredItem.length > 0) {
          this.listItems = filteredItem;
        }
        else {
          this.listItems = this.listItemsFromDb;
          this.nextChar = '';
        }
      }
    }
    this.isListItemSelected = false;
  }

  onItemSelect(data: any) {
    this.mycontent = this.mycontent
      .replace('@@' + this.nextChar, data.id)
      .replace('@@' + this.nextChar, data.id);
    this.isListItemSelected = true;
    this.isListVisible = false;
  }

  change(val){
    console.log("chagned" + val.templateName);
    console.log("chagned" + this.selectedTemplate.templateName);
    this.mycontent = this.selectedTemplate.templateHtml;
  }

  onEdit(){
    this.isEditing = true;
  }
  onSave(){
    this.isEditing = false;
  }

  ngOnDestroy(){

  }

  onSend() {
   this.isSend = true;
   this.isEditing = false;
  }
}
