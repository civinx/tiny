import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MessageService } from './message.service';
import { Observable, of } from 'rxjs';
import { Record } from './record';
import { catchError, map, tap } from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  responsType: 'json'
};

@Injectable({
  providedIn: 'root'
})

export class RecordService {

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  private log(message: string) {
    this.messageService.add(`${message}`);
  }  

  // private recordUrl = 'http://127.0.0.1:8000/tiny/';
  private recordUrl = 'http://47.100.57.37:8000/tiny/';

  generate (record: Record): Observable<Record> {
    return this.http.post<Record>(this.recordUrl, record, httpOptions)
    .pipe(
      tap((record: Record) => this.log('原网址: '+record.old_url + '\t 短网址: '+record.tiny_url)),
      // catchError(this.handleError<Record>('generate'))
    )
  }

  getHeroes(): Observable<Record[]> {
    return this.http.get<Record[]>(this.recordUrl)
      .pipe(
        tap(heroes => this.log('feched heroes')),
        // catchError(this.handleError('getHeroes', []))
      );
  }

  /**
 * Handle Http operation that failed.
 * Let the app continue.
 * @param operation - name of the operation that failed
 * @param result - optional value to return as the observable result
 */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
