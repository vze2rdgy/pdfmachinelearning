import { Overlay, OverlayConfig } from "@angular/cdk/overlay";
import { ViewContainerRef } from "@angular/core";
import { ComponentPortal } from "@angular/cdk/portal";
import { LynxProcessingOverlayComponent } from "./lynx-processing-overlay/lynx-processing-overlay.component";


export abstract class BaseComponent {
    overlayRef = null;
    processing: boolean = false;

    constructor(
        public overlay: Overlay, 
        public viewContainerRef: ViewContainerRef 
    ) { }

    openInProgessOverlay(){
        let config = new OverlayConfig();

        config.positionStrategy = this.overlay.position()
        .global()
        .centerHorizontally()
        .centerVertically();

        config.hasBackdrop = true;

        this.overlayRef = this.overlay.create(config);

        this.overlayRef.backdropClick().subscribe(() => {
            // this.overlayRef.dispose();
          });
          this.overlayRef.attach(new ComponentPortal(LynxProcessingOverlayComponent, this.viewContainerRef));
    }
    closeInProgessOverlay(){
        this.overlayRef.dispose();
    }
}
