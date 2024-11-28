import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MudComponent } from './mud.component';

describe('MudComponent', () => {
  let component: MudComponent;
  let fixture: ComponentFixture<MudComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MudComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MudComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
