import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  Input
} from '@angular/core';
import * as ClassicEditor from '@ckeditor/ckeditor5-build-classic';

@Component({
  selector: 'lynx-htmleditor',
  templateUrl: './htmleditor.component.html',
  styleUrls: ['./htmleditor.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HtmleditorComponent implements OnInit {
  public Editor = ClassicEditor;

  @Input() data = '';
  @Input() isDisabled = false;

  constructor() {}

  ngOnInit() {}
}
