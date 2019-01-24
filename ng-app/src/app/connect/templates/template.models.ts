import { HttpErrorResponse } from "@angular/common/http";

export interface Template {
    templateId: string,
    templateName: string,
    templateHtml: string
}

export interface ConnectTemlatesState {
    retrieveReqTimeStamp?: string;
    templatesResponse: TemplateResponse
}

export interface TemplateResponse {
    templates: Template[],
    error?: HttpErrorResponse
}
