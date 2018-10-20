import { Component, OnInit } from '@angular/core';
import { Record } from '../record';
import { RecordService } from '../record.service';


@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})

export class InputComponent implements OnInit {

  constructor(private recordService: RecordService) { }

  ngOnInit() {
  }

  records: Record[];

  generate(old_url: string): void {
      old_url = old_url.trim();
      if (!old_url) { return; }
      let record = new Record();
      record.old_url = old_url;
      this.recordService.generate(record)
      .subscribe(record => this.records.push(record));
  }



}
