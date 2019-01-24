import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'processing-overlay',
  templateUrl: './processing-overlay.component.html',
  styleUrls: ['./processing-overlay.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProcessingOverlayComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
